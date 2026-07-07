ARG RUST_VERSION=1.88.0-trixie


FROM rust:${RUST_VERSION} AS builder

WORKDIR /app

# Copy source and build in release mode
COPY . .
RUN cargo build --release

# Runtime stage: minimal final image
FROM debian:trixie-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Copy only the compiled binary from the build stage
COPY --from=builder /app/target/release/simeis-server .

# Document that the service listens on port 8080
EXPOSE 8080

# Start the server
CMD ["./simeis-server"]