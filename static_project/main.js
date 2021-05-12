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
    init(0);
}

function onPlayerStateChange(event) {
    var currentVideoId = player.getPlaylistIndex();
    if (event.data == YT.PlayerState.ENDED) {
        if (currentVideoId < videoIDs.length - 1) {
            player.nextVideo();
        }else{
            player.playVideoAt(0);
        }
    }
    init(currentVideoId);
}

function playVideo(videoIndex){
    player.playVideoAt(videoIndex);
}

function init(videoIndex){
    author_username = document.getElementById("author_username");
    var upperName = authorList[videoIndex].charAt(0).toUpperCase() + authorList[videoIndex].slice(1);
    author_username.innerHTML =  upperName;
    author_username.setAttribute('href', authorURLList[videoIndex] );
    post_id = document.getElementById("remove_post_id");
    post_id.value = postPKList[videoIndex];
    var videoIDInput = document.getElementById("videoIDInput");
    videoIDInput.value = "";
    if (authorList[videoIndex] != username ) {
        document.getElementById("removeButton").style.display = "none";
        document.getElementById("shareButton").style.display = "inline";
    }else{
        document.getElementById("removeButton").style.display = "inline";
        document.getElementById("shareButton").style.display = "none";
    }
}

function playNext(){
    var currentVideoId = player.getPlaylistIndex();
    if (currentVideoId < videoIDs.length - 1) {
        player.nextVideo();
    }else{
        player.playVideoAt(0);
    }
}

$("#shareButton").click(function(){
    var currentVideoId = player.getPlaylistIndex();
    var videoID = videoIDs[currentVideoId];
    var videoIDInput = document.getElementById("videoIDInput");
    videoIDInput.value = videoID;
    $("#videoIDInput").transition('tada');
    $("#videoPostButton").transition('tada');
});