exports.data = {
    add_user: {
        first_name: 'Test',
        last_name: 'User',
        email: 'test-windows-firefox@example.org',
        password: 'password'
    },
    modify_user: {
        first_name: 'Testing Firefox Windows',
        last_name: 'Users 2'
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
    add_multipage: {
        name: 'Chrome Mac Multipage',
        url: 'chrome-mac-page/chrome-mac-multipage',
        parent: 'Chrome Mac Page',
        type: 'MultiPage',
        published: true,
        show_in_menu: false,
        file_path: 'multipage.zip'
    },
    add_file: {
        name: 'Firefox Windows File',
        url: 'firefox-windows-page/firefox-windows-file',
        parent: 'Firefox Windows Page',
        type: 'File',
        published: true,
        show_in_menu: false,
        file_path: 'test-service.txt'
    },
    migration_download: {
        name: 'Firefox Windows Download Migration'
    }
};