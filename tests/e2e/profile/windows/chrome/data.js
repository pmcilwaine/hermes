exports.data = {
    add_user: {
        first_name: 'Test',
        last_name: 'User',
        email: 'test-windows-chrome@example.org',
        password: 'password'
    },
    add_page: {
        name: 'Chrome Windows Page',
        menutitle: 'Chrome Windows Page',
        url: 'chrome-windows-page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    add_page_parent: {
        name: 'Chrome Windows Page Parent',
        menutitle: 'Chrome Windows Page Parent',
        url: 'chrome-windows-page/child-page',
        parent: 'Chrome Windows Page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    migration_download: {
        name: 'Chrome Windows Download Migration'
    }
};