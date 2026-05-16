"""
VoiceBox client for OpenClaw.
Controls VoiceBox TTS API at http://127.0.0.1:17493

Capabilities:
- Generate TTS speech
- List/load/download models
- Manage voices/profiles
- Transcribe audio
- Stream speech

Usage:
    from utils.voicebox import VoiceBox
    
    vb = VoiceBox()
    vb.download_model("luxtts")  # CPU-friendly
    vb.load_model("luxtts")
    result = vb.speak("Xin chao, toi la tro ly AI")
    # result contains audio path
    
Models available:
- luxtts (CPU-friendly, fast)
- chatterbox-tts (multilingual)
- qwen-tts-0.6B / 1.7B (quality)
- kokoro (tiny, 82M params)
- whisper-* (transcription, whisper-large already downloaded)
"""
import os
import json
import time
import logging
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List, Union

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "http://127.0.0.1:17493"
DEFAULT_TIMEOUT = 60  # seconds for model operations
GENERATE_TIMEOUT = 120  # seconds for TTS generation


class VoiceBoxError(Exception):
    """VoiceBox API error."""
    pass


class VoiceBox:
    """Client for VoiceBox TTS API."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self._cache_dir = os.path.expandvars(r"%APPDATA%\sh.voicebox.app")

    def _request(
        self,
        method: str,
        path: str,
        data: Any = None,
        timeout: int = DEFAULT_TIMEOUT,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make HTTP request to VoiceBox API."""
        url = f"{self.base_url}{path}"
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Content-Type", "application/json") if body else None
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                if raw:
                    return json.loads(raw.decode("utf-8"))
                return {"status": resp.status}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            logger.error("VoiceBox HTTP %d: %s", e.code, body)
            raise VoiceBoxError(f"HTTP {e.code}: {body}") from e
        except urllib.error.URLError as e:
            logger.error("VoiceBox connection failed: %s", e)
            raise VoiceBoxError(f"Connection failed: {e}") from e

    # ---- Health & Status ----

    def health(self) -> Dict[str, Any]:
        """Check VoiceBox health."""
        return self._request("GET", "/health")

    def status(self) -> Dict[str, Any]:
        """Get full API status."""
        return self._request("GET", "/")

    # ---- Model Management ----

    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models with their status."""
        data = self._request("GET", "/models/status")
        return data.get("models", [])

    def download_model(self, model_name: str = "luxtts") -> Dict[str, Any]:
        """Download a model. Blocks until complete.

        Args:
            model_name: e.g. luxtts, qwen-tts-0.6B, kokoro, chatterbox-tts

        Returns:
            Download status.
        """
        # Check current progress before starting
        progress = self._request("GET", f"/models/progress/{model_name}")
        if progress.get("status") == "downloading":
            logger.info("Model %s already downloading, waiting...", model_name)
            self._wait_for_download(model_name)
            return {"model_name": model_name, "status": "downloaded"}

        logger.info("Downloading model: %s...", model_name)
        result = self._request("POST", "/models/download", {"model": model_name}, timeout=300)
        if result.get("status") == "already_downloaded":
            logger.info("Model %s already downloaded", model_name)
            return result

        # Wait for download to complete
        self._wait_for_download(model_name)
        return self._request("GET", f"/models/progress/{model_name}")

    def _wait_for_download(self, model_name: str, poll_interval: int = 5, max_wait: int = 600):
        """Poll download progress until complete."""
        for _ in range(max_wait // poll_interval):
            progress = self._request("GET", f"/models/progress/{model_name}")
            status = progress.get("status", "")
            if status == "error":
                raise VoiceBoxError(f"Download failed for {model_name}: {progress}")
            if status == "complete" or progress.get("downloaded"):
                logger.info("Model %s download complete", model_name)
                return
            pct = progress.get("progress", 0)
            speed = progress.get("speed_mbps", 0)
            logger.info("Downloading %s: %.1f%% (%s Mbps)", model_name, pct, speed)
            time.sleep(poll_interval)
        raise VoiceBoxError(f"Download timeout for {model_name}")

    def load_model(self, model_name: str) -> Dict[str, Any]:
        """Load a model into memory.

        For TTS, common choices:
        - luxtts (CPU-friendly, fast)
        - qwen-tts-0.6B (good quality)
        - kokoro (tiny, 82M)
        """
        logger.info("Loading model: %s...", model_name)
        
        # For large downloaded models, you can specify size
        model_sizes = {
            "qwen-tts-1.7B": "1.7B",
            "qwen-tts-0.6B": "0.6B",
            "qwen-custom-voice-1.7B": "1.7B",
            "qwen-custom-voice-0.6B": "0.6B",
        }
        size = model_sizes.get(model_name, "")
        
        params = {"model_name": model_name}
        if size:
            params["model_size"] = size

        result = self._request("POST", "/models/load", params, timeout=300)
        logger.info("Model loaded: %s", model_name)
        return result

    def unload_model(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Unload a model from memory."""
        if model_name:
            return self._request("POST", f"/models/{model_name}/unload", timeout=30)
        return self._request("POST", "/models/unload", timeout=30)

    # ---- TTS Generation ----

    def speak(self, text: str, voice: str = "default", **kwargs) -> Dict[str, Any]:
        """Generate speech and play it.

        Args:
            text: Text to speak
            voice: Voice/profile ID (or channel preset)
            **kwargs: Extra params passed to generate endpoint

        Returns:
            Generation result with generation_id and audio info.
        """
        data = {
            "text": text,
            "voice": voice,
            **kwargs,
        }
        return self._request("POST", "/speak", data, timeout=GENERATE_TIMEOUT)

    def generate(self, text: str, **kwargs) -> Dict[str, Any]:
        """Generate speech without playing.

        Args:
            text: Text to synthesize
            **kwargs: 
                voice (str): Voice/profile
                temperature (float): 0.0-1.0
                speed (float): 0.5-2.0
                format (str): wav, mp3, ogg

        Returns:
            Generation result with generation_id, audio_url
        """
        data = {
            "text": text,
            **kwargs,
        }
        result = self._request("POST", "/generate", data, timeout=GENERATE_TIMEOUT)
        
        # If generation is async, poll until ready
        gen_id = result.get("generation_id")
        if gen_id:
            return self._wait_for_generation(gen_id)
        return result

    def generate_stream(self, text: str, **kwargs) -> str:
        """Generate streaming speech, returns URL for SSE stream.

        Returns:
            SSE stream URL
        """
        data = {"text": text, **kwargs}
        result = self._request("POST", "/generate/stream", data, timeout=GENERATE_TIMEOUT)
        return result.get("stream_url", "")

    def get_audio(self, generation_id: str) -> bytes:
        """Download generated audio as bytes."""
        url = f"{self.base_url}/audio/{generation_id}"
        with urllib.request.urlopen(url, timeout=GENERATE_TIMEOUT) as resp:
            return resp.read()

    def save_audio(self, generation_id: str, output_path: str) -> str:
        """Save generated audio to file."""
        audio = self.get_audio(generation_id)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(audio)
        logger.info("Audio saved to %s (%d bytes)", output_path, len(audio))
        return output_path

    def _wait_for_generation(self, gen_id: str, poll_interval: int = 1, max_wait: int = 120) -> Dict:
        """Poll generation status until complete."""
        for _ in range(max_wait // poll_interval):
            status = self._request("GET", f"/generate/{gen_id}/status")
            if status.get("status") == "complete":
                return self._request("GET", f"/history/{gen_id}")
            if status.get("status") in ("failed", "error"):
                raise VoiceBoxError(f"Generation failed: {status}")
            time.sleep(poll_interval)
        raise VoiceBoxError(f"Generation timeout for {gen_id}")

    # ---- Profile/Voice Management ----

    def list_profiles(self) -> List[Dict[str, Any]]:
        """List all voice profiles."""
        return self._request("GET", "/profiles")

    def create_profile(self, name: str, **kwargs) -> Dict[str, Any]:
        """Create a new voice profile."""
        data = {"name": name, **kwargs}
        return self._request("POST", "/profiles", data)

    def get_profile(self, profile_id: str) -> Dict[str, Any]:
        """Get profile details."""
        return self._request("GET", f"/profiles/{profile_id}")

    # ---- Transcription ----

    def transcribe(self, audio_path: str, **kwargs) -> Dict[str, Any]:
        """Transcribe audio file to text.

        Uses Whisper model (whisper-large already downloaded).
        """
        import mimetypes
        from urllib.parse import urlencode

        # Determine content type
        mime, _ = mimetypes.guess_type(audio_path)
        if not mime:
            mime = "audio/wav" if audio_path.endswith(".wav") else "audio/mpeg"

        # Read file
        with open(audio_path, "rb") as f:
            audio_data = f.read()

        # Build multipart request manually
        boundary = "----VoiceBoxBoundary" + str(time.time()).replace(".", "")
        body = []
        body.append(f"--{boundary}".encode())
        body.append(b'Content-Disposition: form-data; name="file"; filename="' + 
                    os.path.basename(audio_path).encode() + b'"')
        body.append(f"Content-Type: {mime}".encode())
        body.append(b"")
        body.append(audio_data)

        for key, value in kwargs.items():
            body.append(f"--{boundary}".encode())
            body.append(f'Content-Disposition: form-data; name="{key}"'.encode())
            body.append(b"")
            body.append(str(value).encode())

        body.append(f"--{boundary}--".encode())
        body_data = b"\r\n".join(body)

        url = f"{self.base_url}/transcribe"
        req = urllib.request.Request(url, data=body_data, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

        try:
            with urllib.request.urlopen(req, timeout=GENERATE_TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise VoiceBoxError(f"Transcribe failed: {e.read().decode()}") from e

    # ---- History ----

    def list_history(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """List recent generations."""
        return self._request("GET", f"/history?limit={limit}&offset={offset}")

    def get_generation(self, gen_id: str) -> Dict[str, Any]:
        """Get generation details."""
        return self._request("GET", f"/history/{gen_id}")

    # ---- Quick workflow ----

    def setup(self, model: str = "luxtts") -> bool:
        """Quick setup: download + load a model.

        Returns True if successful, False otherwise.
        """
        logger.info("VoiceBox setup: downloading model %s...", model)
        try:
            # Check if already downloaded
            models = self.list_models()
            target = next((m for m in models if m["model_name"] == model), None)
            
            if not target:
                logger.error("Model %s not found in available models", model)
                return False

            if not target.get("downloaded"):
                logger.info("Downloading %s...", model)
                self.download_model(model)

            if not target.get("loaded"):
                logger.info("Loading %s...", model)
                self.load_model(model)
                # Wait a moment for model to fully load
                time.sleep(2)

            logger.info("VoiceBox ready with %s", model)
            return True
        except VoiceBoxError as e:
            logger.error("VoiceBox setup failed: %s", e)
            return False
        except Exception as e:
            logger.error("VoiceBox setup error: %s", e)
            return False

    def __repr__(self) -> str:
        return f"VoiceBox(base_url={self.base_url})"
