md2po = find_program('md2po', required: false)

run_target('gameeky-docs-pot',
  command : [
    md2po,
    '..' / 'docs' / 'basics' / 'en' / 'index.md',
    '-dProject-Id-Version: gameeky',
    '-dContent-Type: text/plain; charset=UTF-8',
    '--quiet',
    '--save',
    '--po-encoding=UTF8',
    '--po-filepath=' + '..' / 'docs'/ 'basics' / 'po' / 'gameeky.pot',
  ]
)

msgmerge = find_program('msgmerge', required: false)

run_target('gameeky-docs-update-po',
  command : [
    msgmerge,
    '--previous',
    '--update',
    '--backup=none',
    '..' / 'docs' / 'basics' / 'po' / 'es.po',
    '..' / 'docs' / 'basics' / 'po' / 'gameeky.pot',
  ]
)

translations = [
  'es',
]

po2md = find_program('po2md', required: true, disabler: true)

foreach translation : translations
  run_command(
    po2md,
    'basics' / 'en' / 'index.md',
    '--pofiles=' + 'basics' / 'po' / translation + '.po',
    '--wrapwidth=0',
    '--quiet',
    '--save',
    'basics' / translation / 'index.md',
    check: true,
  )
endforeach

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