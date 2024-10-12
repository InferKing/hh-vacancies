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
        {
            onClick: onClick,
            className: 'btn btn-primary rounded-circle d-flex align-items-center justify-content-center fw-bold',
            style: {
                color: 'white', 
                width: '28px', 
                height: '28px',
                position: 'relative',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)'
            }
        },
        React.createElement('i', { className: 'bi bi-arrow-up-right-circle' })
    )

    // return React.createElement(
    //     'button',
    //     {onClick: onClick, className: 'btn btn-primary d-block w-100 h-100', style: {color: 'white', borderRadius: '0'}},
    //     'Подробнее'
    // );
}