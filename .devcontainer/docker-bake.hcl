group "default" {
  targets = ["greenova"]
}

// Single target for simplicity
target "greenova" {
  context = "."
  dockerfile = ".devcontainer/Dockerfile"
  cache-from = ["type=local,src=.cache/buildx"]
  cache-to = ["type=local,dest=.cache/buildx,mode=max"]
  tags = ["greenova:latest"]
}
