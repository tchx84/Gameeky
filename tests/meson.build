src_dir = join_paths(meson.project_source_root(), 'src')
tests_dir = join_paths(meson.project_source_root(), 'tests')
data_dir = join_paths(tests_dir, 'data')

pyflakes = find_program('pyflakes', required: false)
if pyflakes.found()
  test('pyflakes', pyflakes,
    args: [src_dir, tests_dir])
endif

black = find_program('black', required: false)
if black.found()
  test('black', black,
    args: ['--check', src_dir, tests_dir])
endif

mypy = find_program('mypy', required: false)
if mypy.found()
  test('mypy', mypy,
    args: ['--ignore-missing-imports', src_dir, tests_dir])
endif

pytest = find_program('pytest', required: false)
if pytest.found()
  test('pytest', pytest,
    timeout: 0,
    args: ['--capture=no', '--verbose', tests_dir],
    env : [ 'PYTHONPATH=' + src_dir, 'PROJECT_PATH=' + data_dir])
endif
