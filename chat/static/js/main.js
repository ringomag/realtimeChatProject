console.log('ucitan js')

document.querySelector('#room-name').focus();
document.querySelector('#room-name').onkeyup = function(e){
    if (e.keyCode == 13){
        document.querySelector('#room-name-submit').click();
    }
};
document.querySelector('#room-name-submit').onclick = function(e){
    var roomName = document.querySelector('#room-name').value;
    window.location.pathname = '/chat/' + roomName + '/';
};
