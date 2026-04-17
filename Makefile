build:
	RUSTFLAGS="-C code-model=kernel -C codegen-units=1" cargo build --verbose
