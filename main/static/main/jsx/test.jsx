function Test() {
    const [color, setColor] = React.useState("red");

    return (
        <>
            <h1>Testing!</h1>
            <p>My favourite colour is {color}</p>
            <button
                type="button"
                onClick={() => setColor("red")}
            >Red</button>
            <button
                type="button"
                onClick={() => setColor("green")}
            >Green</button>
            <button
                type="button"
                onClick={() => setColor("blue")}
            >Blue</button>
        </>
    );
}