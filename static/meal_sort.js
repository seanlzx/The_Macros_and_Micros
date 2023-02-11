document.querySelector("#meal_sort input[value='newest']").addEventListener("click", event=> {
    event.preventDefault();
    from = document.querySelector("#meal_sort input[name='from']").value
    to = document.querySelector("#meal_sort input[name='to']").value
    $.ajax({
        type:'get',
        url:'/meal_sort/DESC',
        data:{
            from,
            to
        },
        success:function(response)
        {
            $("#meal_records").html(response);
        }
    })
})

document.querySelector("#meal_sort input[value='oldest']").addEventListener("click", event=> {
    event.preventDefault();
    from = document.querySelector("#meal_sort input[name='from']").value
    to = document.querySelector("#meal_sort input[name='to']").value
    $.ajax({
        type:'get',
        url:'/meal_sort/ASC',
        data:{
            from,
            to
        },
        success:function(response)
        {
            $("#meal_records").html(response);
        }
    })
})