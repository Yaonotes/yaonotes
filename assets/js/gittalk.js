const gitalk = new Gitalk({
    clientID: '6952102337c1db123c4b',
    clientSecret: '224a5a032556d011ab555a48224e938b0146e037',
    repo: 'yaonotes',
    owner: 'xzyaoi',
    admin: ['xzyaoi'],
    id: location.pathname,      // Ensure uniqueness and length less than 50
    distractionFreeMode: true  // Facebook-like distraction free mode
})

function renderComment() {
    gitalk.render('gitalk-container')
}