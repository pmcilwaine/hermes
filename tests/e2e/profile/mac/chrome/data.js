exports.data = {
    add_user: {
        first_name: 'Test',
        last_name: 'User',
        email: 'test-mac-chrome@example.org',
        password: 'password'
    },
    modify_user: {
        first_name: 'Testing Chrome Mac',
        last_name: 'Users 2'
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
    add_file: {
        name: 'Chrome Mac File',
        url: 'chrome-mac-page/chrome-mac-file',
        parent: 'Chrome Mac Page',
        type: 'File',
        published: true,
        show_in_menu: false,
        file_path: 'test-service.txt'
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
    migration_download: {
        name: 'Chrome Mac Download Migration'
    }
};