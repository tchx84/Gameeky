launcher_desktop_file = i18n.merge_file(
        input: 'dev.tchx84.Gameeky.desktop.in',
       output: 'dev.tchx84.Gameeky.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

player_desktop_file = i18n.merge_file(
        input: 'dev.tchx84.Gameeky.Player.desktop.in',
       output: 'dev.tchx84.Gameeky.Player.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

scene_desktop_file = i18n.merge_file(
        input: 'dev.tchx84.Gameeky.Scene.desktop.in',
       output: 'dev.tchx84.Gameeky.Scene.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

entity_desktop_file = i18n.merge_file(
        input: 'dev.tchx84.Gameeky.Entity.desktop.in',
       output: 'dev.tchx84.Gameeky.Entity.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [launcher_desktop_file])
  test('Validate desktop file', desktop_utils, args: [player_desktop_file])
  test('Validate desktop file', desktop_utils, args: [scene_desktop_file])
  test('Validate desktop file', desktop_utils, args: [entity_desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'dev.tchx84.Gameeky.metainfo.xml.in',
       output: 'dev.tchx84.Gameeky.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

install_data('dev.tchx84.Gameeky.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])

subdir('icons')
