module.exports = {
  types: [
    { value: ':sparkles: feat', name: '✨ feat:     A new feature/增加新功能' },
    { value: ':bug: fix', name: '🐛 fix:      A bug fix/缺陷修复' },
    { value: ':pencil: docs', name: '📝 docs:     Documentation only changes/文档修改' },
    {
      value: ':art: style',
      name:
        '💄 style:    Changes that do not affect the meaning of the code/代码风格修改\n              (white-space, formatting, missing semi-colons, etc)',
    },
    {
      value: ':recycle: refactor',
      name: '♻ refactor: A code change that neither fixes a bug nor adds a feature/代码重构',
    },
    {
      value: ':zap: perf',
      name: '⚡ perf:     A code change that improves performance/性能优化',
    },
    { value: ':white_check_mark: test', name: '✅ test:     Adding missing tests/增加测试代码' },
    {
      value: ':pencil2: chore',
      name:
        '🎫 chore:    Changes to the build process or auxiliary tools\n              and libraries such as documentation generation/其他更新',
    },
    { value: ':rewind: revert', name: '⏪ revert:   Revert to a commit/回滚' },
    { value: ':rocket: build', name: '👷 build:    Changes that affect the build system or external dependencies/系统部署相关\n              (example scopes: gulp, broccoli, npm)' },
    { value: ':construction_worker: ci', name: '🔧 ci:       Changes to our CI configuration files and scripts/增加持续集成\n              (example scopes: Travis, Circle, BrowserStack, SauceLabs)'}
  ],

  // scopes: [{ name: 'accounts' }, { name: 'admin' }, { name: 'exampleScope' }, { name: 'changeMe' }],

  allowTicketNumber: false,
  isTicketNumberRequired: false,
  // ticketNumberPrefix: 'TICKET-',
  ticketNumberRegExp: '\\d{1,5}',

  // it needs to match the value for field type. Eg.: 'fix'
  /*
  scopeOverrides: {
    fix: [

      {name: 'merge'},
      {name: 'style'},
      {name: 'e2eTest'},
      {name: 'unitTest'}
    ]
  },
  */
  // override the messages, defaults are as follows
  messages: {
    type: "Select the type of change that you're committing:",
    scope: '\nDenote the SCOPE of this change (optional):',
    // used if allowCustomScopes is true
    customScope: 'Denote the SCOPE of this change:',
    subject: 'Write a SHORT, IMPERATIVE tense description of the change:\n',
    body: 'Provide a LONGER description of the change (optional). Use "|" to break new line:\n',
    breaking: 'List any BREAKING CHANGES (optional):\n',
    footer: 'List any ISSUES CLOSED by this change (optional). E.g.: #31, #34:\n',
    confirmCommit: 'Are you sure you want to proceed with the commit above?',
  },

  // allowCustomScopes: true,
  allowBreakingChanges: ['feat', 'fix'],
  // skip any questions you want
  // skipQuestions: ['body'],

  // limit subject length
  subjectLimit: 100,
  // breaklineChar: '|', // It is supported for fields body and footer.
  // footerPrefix : 'ISSUES CLOSED:'
  // askForBreakingChangeFirst : true, // default is false
};