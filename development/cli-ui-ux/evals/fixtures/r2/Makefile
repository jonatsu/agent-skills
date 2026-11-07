.PHONY: check index

# CI runs `make check` on every push.
check:
	./bm list | head -n 1 | grep -q '^NAME '
	./bm list | grep -q '^clig '

index:
	./scripts/export-names.sh
