po4a = find_program('po4a')

env = environment()
env.set('PERL5LIB', get_option('prefix') / get_option('libdir') / 'perl5'/ 'site_perl')

run_command(po4a, '--no-update', 'po4a.cfg', check: true, env: env)
