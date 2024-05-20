pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

docs = [
  'basics/html/en/index.html',
  'basics/html/es/index.html',
  'basics/html/hi/index.html',
  'basics/html/nl/index.html',
  'basics/html/pt_BR/index.html',
]

install_data(
  docs,
  install_dir: pkgdatadir / 'docs',
  preserve_path: true,
 )

install_symlink(
  'src',
  install_dir: pkgdatadir,
  pointing_to: pkgdatadir,
)
