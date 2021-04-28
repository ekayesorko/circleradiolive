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
    author_image = document.getElementById("author_image");
    author_image.src = authorImageList[currentVideoId];
    author_username = document.getElementById("author_username");
    author_username.innerHTML = "suggested by " + authorList[currentVideoId];
}