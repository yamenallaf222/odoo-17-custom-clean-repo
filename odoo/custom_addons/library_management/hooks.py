def post_init_create_depreciation_cron(env):
        env['library.book']._create_depreciation_cron()
