# Docker Inspection Summary

## Running Containers

| Container | Image | Status | Ports | Volume | Type |
|---|---|---|---|---|---|
| **qdrant** | qdrant/qdrant | Up 25m | 6333-6334 | `E:\KY-DATA\Data\qdrant_storage` | Database |
| **openclaw-tinyproxy** | vimagick/tinyproxy | Up 2h | 1080->8888 | None | Tool |
| **dozzle** | amir20/dozzle | Up 2h | 8888->8080 | /var/run/docker.sock | Monitor |
| **portainer** | portainer/portainer-ce | Up 2h | 9000->9000 | portainer_data + docker.sock | Monitor |

## Non-Running Containers

| Container | Image | Status | Note |
|---|---|---|---|
| **n8n-pro** | n8nio/n8n | Restarting loop | 2.27GB image, may be misconfigured |
| **image-python-worker** | 099b4b70198b | Exited 2h ago | ML pipeline worker |

## Images (9 total)

| Image | Size | Used By | Note |
|---|---|---|---|
| n8nio/n8n:latest | 2.27GB | n8n-pro | Restarting |
| n8n-pipeline-python-worker:latest | 1.34GB | — | Not running, might be unused |
| ghcr.io/langfuse/langfuse:latest | 1.37GB | — | Not running, LLM observability |
| postgres:16-alpine | 396MB | — | Not running, for n8n |
| portainer/portainer-ce:latest | 242MB | portainer | Active |
| python:3.11-slim | 188MB | — | Sandbox testing |
| qdrant/qdrant:latest | ~200MB | qdrant | Active |
| amir20/dozzle:latest | 89MB | dozzle | Active |
| alpine:latest | 13MB | — | Utility |
| vimagick/tinyproxy:latest | 9MB | tinyproxy | Active |

## Network

| Network | Driver | Containers |
|---|---|---|
| bridge (default) | bridge | All |
| host | host | N/A |
| none | null | N/A |

## Volumes

| Volume | Driver | Used By |
|---|---|---|
| portainer_data | local | portainer |

## Recommendations

1. **Fix or remove n8n**: 2.27GB image không dùng được (restart loop). Cần debug hoặc xóa.
2. **Clean unused images**: langfuse (1.37GB), n8n-pipeline-python-worker (1.34GB) không chạy.
3. **Add docker-compose.yml**: Để reproduce services dễ dàng.
4. **Restart policy**: Qdrant, dozzle, portainer đang chạy manual, nên thêm `--restart always`.
