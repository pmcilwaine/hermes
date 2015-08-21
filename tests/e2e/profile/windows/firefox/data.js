exports.data = {
    add_user: {
        first_name: 'Test',
        last_name: 'User',
        email: 'test-windows-firefox@example.org',
        password: 'password'
    },
    add_page: {
        name: 'Firefox Windows Page',
        menutitle: 'Firefox Windows Page',
        url: 'firefox-windows-page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    add_page_parent: {
        name: 'Firefox Windows Page Parent',
        menutitle: 'Firefox Windows Page Parent',
        url: 'firefox-windows-page/child-page',
        parent: 'Firefox Windows Page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    add_file: {
        name: 'Firefox Windows File',
        url: 'firefox-windows-page/firefox-windows-file',
        parent: 'Firefox Windows Page',
        type: 'File',
        published: true,
        show_in_menu: false,
        file_path: ''
    },
    migration_download: {
        name: 'Firefox Windows Download Migration'
    }
};