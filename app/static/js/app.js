(function ($) {

    'use strict';

    function initMetisMenu() {
        //metis menu
        $("#side-menu").metisMenu();
    }

    function initCounterNumber() {
        var counter = document.querySelectorAll('.counter-value');
        var speed = 250; // The low means the slower
        counter.forEach(function (counter_value) {
            function updateCount() {
                var target = +counter_value.getAttribute('data-target');
                var count = +counter_value.innerText;
                var inc = target / speed;
                if (inc < 1) {
                    inc = 1;
                }
                // Check if target is reached
                if (count < target) {
                    // Add inc to count and output in counter_value
                    counter_value.innerText = (count + inc).toFixed(0);
                    // Call function every ms
                    setTimeout(updateCount, 1);
                } else {
                    counter_value.innerText = target;
                }
            };
            updateCount();
        });
    }

    function initLeftMenuCollapse() {
        var currentSIdebarSize = document.body.getAttribute('data-sidebar-size');
        $(window).on('load', function () {

            $('.switch').on('switch-change', function () {
                toggleWeather();
            });

            if (window.innerWidth >= 1024 && window.innerWidth <= 1366) {
                document.body.setAttribute('data-sidebar-size', 'sm');
                updateRadio('sidebar-size-small')
            }
        });

        $('#vertical-menu-btn').on('click', function (event) {
            event.preventDefault();
            $('body').toggleClass('sidebar-enable');
            if ($(window).width() >= 992) {
                if (currentSIdebarSize == null) {
                    (document.body.getAttribute('data-sidebar-size') == null || document.body.getAttribute('data-sidebar-size') == "lg") ? document.body.setAttribute('data-sidebar-size', 'sm'): document.body.setAttribute('data-sidebar-size', 'lg')
                } else if (currentSIdebarSize == "md") {
                    (document.body.getAttribute('data-sidebar-size') == "md") ? document.body.setAttribute('data-sidebar-size', 'sm'): document.body.setAttribute('data-sidebar-size', 'md')
                } else {
                    (document.body.getAttribute('data-sidebar-size') == "sm") ? document.body.setAttribute('data-sidebar-size', 'lg'): document.body.setAttribute('data-sidebar-size', 'sm')
                }
            }
        });
    }

    function initMenuItemScroll() {
        // focus active menu in left sidebar
        $(document).ready(function () {
            if ($("#sidebar-menu").length > 0 && $("#sidebar-menu .mm-active .active").length > 0) {
                var activeMenu = $("#sidebar-menu .mm-active .active").offset().top;
                if (activeMenu > 300) {
                    activeMenu = activeMenu - 300;
                    $(".vertical-menu .simplebar-content-wrapper").animate({
                        scrollTop: activeMenu
                    }, "slow");
                }
            }
        });
    }

    function initHoriMenuActive() {
        $(".navbar-nav a").each(function () {
            var pageUrl = window.location.href.split(/[?#]/)[0];
            if (this.href == pageUrl) {
                $(this).addClass("active");
                $(this).parent().addClass("active");
                $(this).parent().parent().addClass("active");
                $(this).parent().parent().parent().addClass("active");
                $(this).parent().parent().parent().parent().addClass("active");
                $(this).parent().parent().parent().parent().parent().addClass("active");
                $(this).parent().parent().parent().parent().parent().parent().addClass("active");
            }
        });
    }

    function initFullScreen() {
        $('[data-toggle="fullscreen"]').on("click", function (e) {
            e.preventDefault();
            $('body').toggleClass('fullscreen-enable');
            if (!document.fullscreenElement && /* alternative standard method */ !document.mozFullScreenElement && !document.webkitFullscreenElement) { // current working methods
                if (document.documentElement.requestFullscreen) {
                    document.documentElement.requestFullscreen();
                } else if (document.documentElement.mozRequestFullScreen) {
                    document.documentElement.mozRequestFullScreen();
                } else if (document.documentElement.webkitRequestFullscreen) {
                    document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
                }
            } else {
                if (document.cancelFullScreen) {
                    document.cancelFullScreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.webkitCancelFullScreen) {
                    document.webkitCancelFullScreen();
                }
            }
        });
        document.addEventListener('fullscreenchange', exitHandler);
        document.addEventListener("webkitfullscreenchange", exitHandler);
        document.addEventListener("mozfullscreenchange", exitHandler);

        function exitHandler() {
            if (!document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement) {
                $('body').removeClass('fullscreen-enable');
            }
        }
    }

    function initDropdownMenu() {
        if (document.getElementById("topnav-menu-content")) {
            var elements = document.getElementById("topnav-menu-content").getElementsByTagName("a");
            for (var i = 0, len = elements.length; i < len; i++) {
                elements[i].onclick = function (elem) {
                    if (elem && elem.target && elem.target.getAttribute("href") === "#") {
                        elem.target.parentElement.classList.toggle("active");
                        if(elem.target.nextElementSibling)
                            elem.target.nextElementSibling.classList.toggle("show");
                    }
                }
            }
            window.addEventListener("resize", updateMenu);
        }
    }

    function updateMenu() {
        var elements = document.getElementById("topnav-menu-content").getElementsByTagName("a");
        for (var i = 0, len = elements.length; i < len; i++) {
            if (elements[i] && elements[i].parentElement && elements[i].parentElement.getAttribute("class") === "nav-item dropdown active") {
                elements[i].parentElement.classList.remove("active");
                if(elements[i].nextElementSibling)
                    elements[i].nextElementSibling.classList.remove("show");
            }
        }
    }

    function initComponents() {
        // tooltip
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        });

        // popover
        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl)
        });

        // toast
        var toastElList = [].slice.call(document.querySelectorAll('.toast'))
        var toastList = toastElList.map(function (toastEl) {
            return new bootstrap.Toast(toastEl)
        })
    }

    function initPreloader() {
        $(window).on('load', function () {
            $('#status').fadeOut();
            $('#preloader').delay(350).fadeOut('slow');
        });
    }

    function initSettings() {
        if (window.sessionStorage) {
            var alreadyVisited = sessionStorage.getItem("is_visited");
            if (!alreadyVisited) {
                sessionStorage.setItem("is_visited", "layout-ltr");
            } else {
                $("#" + alreadyVisited).prop('checked', true);
                // changeDirection(alreadyVisited);
            }
        }
    }

    function initCheckAll() {
        $('#checkAll').on('change', function () {
            $('.table-check .form-check-input').prop('checked', $(this).prop("checked"));
        });
        $('.table-check .form-check-input').change(function () {
            if ($('.table-check .form-check-input:checked').length == $('.table-check .form-check-input').length) {
                $('#checkAll').prop('checked', true);
            } else {
                $('#checkAll').prop('checked', false);
            }
        });
    }


    $('#mode-setting-btn').on('click', function (e) {
        var body = document.getElementsByTagName("body")[0];
        if(body.hasAttribute("data-bs-theme") && body.getAttribute("data-bs-theme") == "dark") {
            document.body.setAttribute('data-bs-theme', 'light');
            document.body.setAttribute('data-topbar', 'light');
            document.body.setAttribute('data-sidebar', 'light');
            (body.hasAttribute("data-layout") && body.getAttribute("data-layout") == "horizontal") ? '' : document.body.setAttribute('data-sidebar', 'light');
        } else {
            document.body.setAttribute('data-bs-theme', 'dark');
            document.body.setAttribute('data-topbar', 'dark');
            document.body.setAttribute('data-sidebar', 'dark');
            (body.hasAttribute("data-layout") && body.getAttribute("data-layout") == "horizontal") ? '' : document.body.setAttribute('data-sidebar', 'dark');
        }
    });

    function init() {
        initMetisMenu();
        initCounterNumber();
        initLeftMenuCollapse();
        initMenuItemScroll();
        initHoriMenuActive();
        initFullScreen();
        initDropdownMenu();
        initComponents();
        initSettings();
        initPreloader();
        Waves.init();
        initCheckAll();
    }

    init();

})(jQuery)


document.addEventListener('DOMContentLoaded', function() {
    feather.replace();
});
