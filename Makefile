SSH ?= qidi
KLIPPER_DIR ?= ~/klipper

STUB_SRC := vendor/klipper-src
STUB_OUT := vendor/stubs

NUITKA_IMAGE ?= q2-nuitka
NUITKA_DIST := dist

.PHONY: check-env setup sync test lint fmt typecheck stub-gen stub-clean \
	nuitka-image build clean

check-env:
	@uv --version

setup: check-env
	@uv sync

sync: setup

test: setup
	@uv run pytest

lint: setup
	@uv run ruff check --fix
	@uv run mypy

fmt: setup
	@uv run ruff format

stub-gen:
	@rm -rf $(STUB_SRC) $(STUB_OUT)
	@mkdir -p $(STUB_SRC) $(STUB_OUT)
	@ssh $(SSH) "tar -C $(KLIPPER_DIR) -cf - \
		--exclude='klippy/extras/q2_loadcell*' \
		--exclude='klippy/extras/qpa_*' \
		--exclude='klippy/extras/autopa' \
		klippy" | tar -C $(STUB_SRC) -xf -
	@find $(STUB_SRC)/klippy -type l ! -exec test -e {} \; -delete
	@uv run stubgen --no-analysis --include-private \
		--search-path $(STUB_SRC)/klippy -o $(STUB_OUT) $(STUB_SRC)/klippy
	@echo "stubs written to $(STUB_OUT)"

stub-clean:
	rm -rf $(STUB_SRC) $(STUB_OUT)

nuitka-image:
	docker buildx build --platform linux/arm64 \
		-f docker/nuitka.Dockerfile -t $(NUITKA_IMAGE) .

build: nuitka-image
	@mkdir -p $(NUITKA_DIST)
	docker run --rm --platform linux/arm64 \
		-u "$$(id -u):$$(id -g)" -e HOME=/tmp \
		-v "$(CURDIR)/src:/src:ro,Z" \
		-v "$(CURDIR)/$(NUITKA_DIST):/dist:Z" \
		$(NUITKA_IMAGE)

clean:
	rm -rf $(NUITKA_DIST) $(STUB_SRC)
