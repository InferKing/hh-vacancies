var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.VacancyLink = function (props) {
    return React.createElement(
        'a',
        {href: props.data["Ссылка"], target: '_blank', style: {color: 'blue'}},
        props.value
    );
};

dagcomponentfuncs.GetMoreInfo = function (props) {

    function onClick() {
        props.setData();
    }

    return React.createElement(
        'button',
        {onClick: onClick, className: 'btn btn-primary d-block w-100 h-100', style: {color: 'white', borderRadius: '0'}},
        'Подробнее'
    );
}