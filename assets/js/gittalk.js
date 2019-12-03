const gitalk = new Gitalk({
    clientID: 'Iv1.d69c729180549526',
    clientSecret: '05ca79722f9106102b4e175e06c0ce2054eb7ed6',
    repo: 'yaonotes',
    owner: 'xzyaoi',
    admin: ['xzyaoi'],
    id: location.pathname,      // Ensure uniqueness and length less than 50
    distractionFreeMode: true  // Facebook-like distraction free mode
})

function renderComment() {
    gitalk.render('gitalk-container')
}