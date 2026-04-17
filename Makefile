.PHONY: build tests check clean modifyTyp

build:
	RUSTFLAGS="-C code-model=kernel -C codegen-units=1" cargo build --verbose

tests : 
	cargo test

check : 
	cargo check

clean : 
	cargo clean

modifyTyp : 
	typst compile doc\manual.typ doc\manual.pdf