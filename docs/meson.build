subdir('po')

languages = [
  'en',
  'es',
]

pandoc = find_program('pandoc', required: true, disabler: true)

foreach language : languages
  run_command(
    pandoc,
    '--standalone',
    '--css=basics/data/style.css',
    '--include-in-header=basics/data/headers.xml',
    '--output=' + 'basics' / language / 'index.html',
     'basics' / language / 'index.md',
    check: true,
  )
endforeach

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