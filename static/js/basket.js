window.onload = function () {



    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let t_href = e.target
        $.ajax(
            {
                url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
                success: function (data) {
                    $('.basket_list').html(data.result)
                },
            });
        e.preventDefault()
    })

    var csrf = $('meta[name="csrf_token"]').attr('content');
    $('.card_add_basket').on('click', 'button[type="submit"]', (e) => {
        let t_href = e.target.post.value
        $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': csrf},
                url: "/baskets/add/" + t_href + "/",
                success: function (data) {
                    $('.card_add_basket').html(data.result);
                    swal('Спасибо!', 'Ваш товар, добавлен в корзину!', 'success')
                },
            });
        e.preventDefault()
    })
}