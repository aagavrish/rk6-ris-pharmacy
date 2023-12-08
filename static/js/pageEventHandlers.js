$(window).on('load', function () {
    setTimeout(function () {
        $('#loading').hide();
    }, 250);

    let currentDate = new Date();
    let maxDateDay = currentDate.toISOString().split('T')[0]; // формат YYYY-MM-DD
    let maxDateMonth = maxDateDay.slice(0, 7); // формат YYYY-MM
    let minDateDay = "2020-01-01"; // формат YYYY-MM-DD для типа date
    let minDateMonth = "2020-01"; // формат YYYY-MM для типа month

    $('input[type="date"]').each(function () {
        $(this).attr('max', maxDateDay);
        $(this).attr('min', minDateDay);
    });

    $('input[type="month"]').each(function () {
        $(this).attr('max', maxDateMonth);
        $(this).attr('min', minDateMonth);
    });
});

$(document).ready(function () {
    var sqlResults = $('.sql-results');
    if (sqlResults.length) {
        sqlResults[0].scrollIntoView({ behavior: "smooth" });
    }

    var message = $('.message');
    var mytable = $('.container-centered');
    if (message.length && mytable.length) {
        message.css('width', mytable.css('width'));
        message.css('maxWidth', mytable.css('width'));
    }

    $(window).on('resize', function () {
        if (message.length && mytable.length) {
            message.css('width', mytable.css('width'));
            message.css('maxWidth', mytable.css('width'));
        }
    });

    $('.cross').on('click', function () {
        window.location.href = '/';
    });
});

$(document).ready(function () {
    $('#search').on('input', function () {
        var searchQuery = $(this).val().toLowerCase();
        var firstRow = true;

        // Проходим по всем строкам таблицы
        $('tbody tr').each(function () {
            var medName = $(this).find('td:first').text().toLowerCase();

            // Если название препарата содержит поисковый запрос, показываем строку
            if (medName.includes(searchQuery)) {
                $(this).show();

                // Если это первая строка, которая отображается, удаляем у нее верхний отступ
                if (firstRow) {
                    $(this).find('td').css('border-top', 'none');
                    firstRow = false;
                } else {
                    // Для всех остальных строк возвращаем верхний отступ
                    $(this).find('td').css('border-top', '');
                }
            } else {
                // Иначе скрываем строку
                $(this).hide();
            }
        });
    });
});