exports.data = {
    add_user: {
        first_name: 'Test',
        last_name: 'User',
        email: 'test-mac-chrome@example.org',
        password: 'password'
    },
    add_page: {
        name: 'Chrome Mac Page',
        menutitle: 'Chrome Mac Page',
        url: 'chrome-mac-page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    add_page_parent: {
        name: 'Chrome Mac Page Parent',
        menutitle: 'Chrome Mac Page Parent',
        url: 'chrome-mac-page/child-page',
        parent: 'Chrome Mac Page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    migration_download: {
        name: 'Chrome Mac Download Migration'
    }
};