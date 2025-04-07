from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #obtener valores del formulario
        fx_str = request.form['funcion']
        x0 = float(request.form['x0'])
        y0 = float(request.form['y0'])
        h = float(request.form['h'])
        n = int(request.form['n'])

        #creacion de variables simbolicas para x,y
        x, y = sp.symbols('x y')
        #convertir ecuacion en expresion simbolica
        f_expr = sp.sympify(fx_str)

        #convertir la ecuacion a una funcion numerica
        f_lambda = sp.lambdify((x, y), f_expr, 'math')

        #creacion de array donde se almacenaran los resultados
        resultados = []

        #asignar valor de Xn
        x_curr = x0
        #asignar valor de Yn
        y_curr = y0

        #bucle que repetira las operaciones hasta completar el numero de pasos
        for i in range(n):
            #calcular valor predicho (Yn+1)*
            y_pred = y_curr + h * f_lambda(x_curr, y_curr)
            #calcular el siguiente valor de x (Xn+1)
            x_next = x_curr + h
            #valor de con correccion Yn+1
            y_corr = y_curr + (h / 2) * (f_lambda(x_curr, y_curr) + f_lambda(x_curr + h, y_pred))

            #se agregan los resultados con cada repeticion del bucle for
            resultados.append((i, x_curr, y_curr, y_pred, x_next, y_corr))

            #se asignan nuevos valores para Xn y Yn
            x_curr = x_next
            y_curr = y_corr

        #finalizadas las operaciones, los resultados se mandan a la plantillia resultados
        return render_template('resultado.html', resultados=resultados)

    #en caso que no se enviaran datos en el formulario se redirije al index
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
