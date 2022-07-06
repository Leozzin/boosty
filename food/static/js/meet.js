const domain = 'meet.jit.si';
const options = {
    roomName: 'jitmeet',
    width: "100%",
    height: "100%",
    parentNode: document.querySelector('#meet'),
    userInfo: {
    	email: "adhemmbarkia@gmail.com",
    	displayName: "Adhem Mbarkia",
    },
};
const api = new JitsiMeetExternalAPI(domain, options);