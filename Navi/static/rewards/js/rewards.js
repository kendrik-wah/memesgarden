function confirmRedeem() {
	window.confirm = function() {
		createCustomConfirm();
	}
};

function createCustomConfirm() {

};