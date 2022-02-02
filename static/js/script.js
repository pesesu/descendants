var  btnToggle =  document.getElementById('nav-toggle')
var sidebar = document.getElementById('sidebar')
var close = document.getElementById('close')

btnToggle.addEventListener('click', function(){
    sidebar.classList.remove('hide')
    sidebar.classList.add('display')
})

close.addEventListener('click', function(){
    sidebar.classList.remove('display')
    sidebar.classList.add('hide')
})
