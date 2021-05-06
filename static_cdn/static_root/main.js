function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        playerVars: {
        controls: 1,
        },
        events: {
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerReady(event) {
    player.loadPlaylist( {
        playlist:videoIDs
    } );
    showMetaData();
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
        if (currentVideoId < videoIDs.length - 1) {
            currentVideoId++;
            player.nextVideo();
        }else{
            currentVideoId = 0;
            player.playVideoAt(0);
        }
    }else if(event.data == YT.PlayerState.PLAYING){
        showMetaData();
    }
}
function playVideo(videoIndex){
    player.playVideoAt(videoIndex);
}
function showMetaData(){
    author_username = document.getElementById("author_username");
    author_username.innerHTML =  authorList[currentVideoId];
    author_username.setAttribute('href', authorURLList[currentVideoId] );
}