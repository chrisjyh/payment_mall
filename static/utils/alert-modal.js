// 모달창 띄우는 함수
// css_selector id 값으로 받아야함
 function AlertModal(css_selector){
    const modal_select = document.querySelector(css_selector);
    const modal = new bootstrap.Modal(css_selector);
    
    this.show = function(message){
        modal_select.querySelector(".modal-body").textContent = message;
        modal.show()
    }
}