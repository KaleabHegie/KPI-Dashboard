"use strict";
let url = `ws://${window.location.host}/ws/socket-server/`;
const chatSocket = new WebSocket(url);
console.log('chatSocket instantiated.');
var currentChatUser = 0;


function scrollChatBox(){
    try{
        document.getElementById('messages').lastElementChild.scrollIntoView();
    } catch(error){
        console.log('error scrolling chat box');
    }
}

function sendMessage(content, user_id){
	$.post('/chat/send-message', {'user_id': user_id, 'content': content}, function (data, status) {
		;
	});
}

function sendMessageSocket(messageContent){
    if (chatSocket.readyState == 1){
        console.log('sending message to server');
        console.log(messageContent);
        chatSocket.send(JSON.stringify({
            'type': 'chat_message',
            'message': messageContent,
            'to': currentChatUser,
        }));
    } else {
        console.log('socket connection failiure; using ajax post request');
        sendMessage(messageContent, currentChatUser);
    }
}


function markAsRead(user_id){
	$.ajax({
		url: '/chat/mark-as-read/'+user_id,
		success: function(result) {
			var count = result['data'];
			var userBox = document.querySelector('#userList'+user_id);
			var messageCount = userBox.querySelector('#unreadMessageCount')
			messageCount.innerText = count;
			// messageCount.classList.add('d-none');
            messageCount.style.display = 'none';
		},
		error: function(){
			console.log('error while markasread');
		}
	})
}

function loadMessages(user_id){
	$.ajax({
		url: '/chat/with-user/'+user_id,
		success: function(result) {
			var html_text = result['data'];
			document.querySelector('#messages').innerHTML = html_text;
            scrollChatBox()
			markAsRead(user_id);
		},
		error: function(){
			console.log('error makeing ajax request')
		}
	})
}

function countNewMessages(user_id){
	$.ajax({
		url: '/chat/new-message-count/'+user_id,
		success: function(result) {
			var count = result['data'];
			if (count !=0 ) {
				var userBox = document.querySelector('#userList'+user_id);
				var messageCount = userBox.querySelector('#unreadMessageCount')
				messageCount.innerText = count;
				messageCount.style.display = 'inline';
			}
		},
		error: function() {
			console.log('error getting unread message count');
		},
	})
}

function activateChatUser(user_id) {
	// disable active icon from prev and activate on the new one
	if (user_id == currentChatUser){
		return;
	}
	chatSocket.send(JSON.stringify({
		'type': 'active_chat',
		'user_id': user_id,
		'prev_user': currentChatUser,
	}))
	try {
		document.querySelector('#userList'+currentChatUser).querySelector('#activeUserIcon').style.display="none";
	} catch(error) {
		;
	}
	// document.querySelector('#userList'+user_id).querySelector('#activeUserIcon').style.display="block";
	// document.querySelector('a#activeUserName').innerText = username;
	currentChatUser = user_id;
	loadMessages(user_id);
}

function handleIncomingSocketMessage(e){
    let data = JSON.parse(e.data);
    console.log('Data:', data);

    if(data.type==='chat'){
        if(data.from != currentChatUser){
            return;
        }
        console.log('new message arrived');
        console.log(data.message);
        document.getElementById('messages').innerHTML += `<div class="message received">${data.message}</div>`;
        scrollChatBox();
        markAsRead(data.from);
    } else if (data.type === 'inbox_update') {
        countNewMessages(data.from);
    }
}

chatSocket.onmessage = handleIncomingSocketMessage;
