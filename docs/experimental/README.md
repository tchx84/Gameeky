# Building and Running Gameeky Launcher

This guide explains how to build and run **Gameeky Launcher** from source using **Meson** and **Ninja**.

---

## 1. Install Dependencies

**macOS (Homebrew):**

```bash
brew install meson pkg-config libadwaita cmake gtksourceview5 desktop-file-utils gstreamer adwaita-icon-theme
````

---

## 2. Configure and Build

Create the build directory and configure Meson:

```bash
meson setup _build --prefix=~/.local -Dwebkit=disabled
```

Then build and install:

```bash
cd _build
ninja install
```

---

## 3. Run Tests (Optional)

```bash
meson test
```

---

## 4. Launch Gameeky

Run the launcher:

```bash
cd ..
GSK_RENDERER=gl ~/.local/bin/dev.tchx84.Gameeky.Launcher
```

If you don't have it already you can add `~/.local/bin` to your `PATH`:

```bash
export PATH=$PATH:~/.local/bin
```
And then run:

```bash
GSK_RENDERER=gl dev.tchx84.Gameeky.Launcher
```

> 💡 `GSK_RENDERER=gl` forces GTK to use OpenGL for rendering, instead of Vulkan.

Another option:
```bash
export GSK_RENDERER=gl
./dist/bin/dev.tchx84.Gameeky.Launcher
```

---

## 5. Install Theme Pack

(Optional) Install the **Freedom Valley** theme pack:

```bash
mkdir -p ~/Gameeky
cd ~/Gameeky
git clone https://github.com/tchx84/FreedomValley.git
```

---

## 6. Done!

You should now have **Gameeky Launcher** running locally with your chosen theme.


