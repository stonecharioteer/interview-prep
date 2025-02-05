# DSA Interview Prep

This is my interview prep repository for DSA. I'm trying to learn these through
repetitive learning, and through Python, typescript and Rust.

I use `uv` for python, `cargo` for Rust and `deno` for typescript.

I use the `justfile` for running tests as I code.

`just run-tests $LANG` runs all tests, in all languages by default. Accepted arguments are `py`, `ts` or `rust`. Default is `all`

`just run-some-tests $FILTER $LANG` accepts filters that it'll pass on to the test runner. Default runs all languages.

## Dependencies
* uv
* deno
* rustup
* just
* gum
