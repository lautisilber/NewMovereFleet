function TextInput({label, props}) {
    return (
        <>
            <label htmlFor={label}>{label}: </label>
            <input type="text" name={label} {...props}/>
        </>
    )
}

function IntInput({label, props}) {
    return (
        <>
            <label htmlFor={label}>{label}: </label>
            <input type="number" name={label} step="1" {...props}/>
        </>
    )
}

function FloatInput({label, props}) {
    return (
        <>
            <label htmlFor={label}>{label}: </label>
            <input type="number" name={label} step="0.0001" {...props}/>
        </>
    )
}

function ChoiceInput({label, props}) {
    const choices = props.choices;
    const propsNoChoice = (({choices, ...o}) => o)(props);

    console.log(choices)

    return (
        <>
            <label htmlFor={label}>{label}: </label>
            <select {...propsNoChoice}>
                {props.choices.map(item => (
                    <option value={item[0]}>{item[1]}</option>
                ))}
            </select>
        </>
    )
}

function SubmitButton({label, props}) {
    return (
        <button type="submit" {...props}>{label}</button>
    )
}

function EditFormBase({props}) {
    // props = [
    //     {label: 'text1', type: 'text', props: {maxLength: '8'}},
    //     {label: 'int1', type: 'int', props: {min: '0'}},
    //     {label: 'float1', type: 'float', props: {max: '10'}},
    //     {label: 'choice1', type: 'choice', props: {choices: [['10', 'Ten'], ['20', 'Twenty'], ['30', 'Thirty']]}},
    // ]

    function getInput(inputType, label, props) {
        if (inputType === 'text') {
            return (
                <TextInput label={label} props={props} />
            )
        } else if (inputType === 'int') {
            return (
                <IntInput label={label} props={props} />
            )
        } else if (inputType === 'float') {
            return (
                <FloatInput label={label} props={props} />
            )
        } else if (inputType === 'choice') {
            return (
                <ChoiceInput label={label} props={props} />
            )
        }
    }

    return (
        <>
            <h1>Test</h1>
            <form action="/" method="post">
                {
                    p.map(item => (
                        <>
                        {getInput(item.type, item.label, item.props)}
                        <br />
                        </>
                    ))
                }
                <SubmitButton label={"Set"} />
            </form>
        </>

    );
}