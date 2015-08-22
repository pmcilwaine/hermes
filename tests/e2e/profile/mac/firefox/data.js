exports.data = {
    add_user: {
        first_name: 'Test',
        last_name: 'User',
        email: 'test-mac-firefox@example.org',
        password: 'password'
    },
    modify_user: {
        first_name: 'Testing',
        last_name: 'Users 2'
    },
    add_page: {
        name: 'Firefox Mac Page',
        menutitle: 'Firefox Mac Page',
        url: 'firefox-mac-page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    add_page_parent: {
        name: 'Firefox Mac Page Parent',
        menutitle: 'Firefox Mac Page Parent',
        url: 'firefox-mac-page/child-page',
        parent: 'Firefox Mac Page',
        type: 'Page',
        published: true,
        show_in_menu: true,
        template: 'Standard',
        content: '<p>Hello World</p>'
    },
    add_file: {
        name: 'Firefox Mac File',
        url: 'firefox-mac-page/firefox-mac-file',
        parent: 'Firefox Mac Page',
        type: 'File',
        published: true,
        show_in_menu: false,
        file_path: 'test-service.txt'
    },
    migration_download: {
        name: 'Firefox Mac Download Migration'
    }
};