pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

docs = [
  'basics/en/index.html',
  'basics/es/index.html',
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