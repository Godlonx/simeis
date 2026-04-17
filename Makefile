.PHONY: build tests check clean modify-typ

build:
	RUSTFLAGS="-C code-model=kernel -C codegen-units=1" cargo build --verbose

tests : 
	cargo test

check : 
	cargo check

clean : 
	cargo clean

modify-typ : 
	typst compile doc/manual.typ doc/manual.pdf