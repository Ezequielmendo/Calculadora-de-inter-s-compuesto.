from flask import Flask, redirect, render_template, request, flash, url_for
import math  # Importamos math para mayor precisión en los cálculos
import secrets

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(20)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            try:
                # Capturar datos del formulario
                capital = float(request.form['capitalinicial'])
                tasainteres = float(request.form['tasa'])
                periodo = int(request.form['periodo'])
                aportemensual = float(request.form['aportemensual'])

                # Cálculos principales
                tasamensual = tasainteres / 100 / 12  # Convertir tasa anual a mensual en decimal
                meses = periodo * 12  # Convertir periodo en años a meses

                # Calcular el monto final usando interés compuesto
                monto_capital = capital * math.pow(1 + tasamensual, meses)
                monto_aportes = aportemensual * ((math.pow(1 + tasamensual, meses) - 1) / tasamensual)
                capitalfinal = round(monto_capital + monto_aportes, 2)

                # Calcular ganancia y total invertido
                inversiontotal = capital + (aportemensual * meses)
                ganancia = round(capitalfinal - inversiontotal, 2)

                # Generar datos para la tabla de resultados
                datos_tabla = []
                for año in range(1, periodo + 1):
                    meses_año = año * 12
                    monto_año_capital = capital * math.pow(1 + tasamensual, meses_año)
                    monto_año_aportes = aportemensual * ((math.pow(1 + tasamensual, meses_año) - 1) / tasamensual)
                    total_año = round(monto_año_capital + monto_año_aportes, 2)
                    inversion_año = capital + (aportemensual * meses_año)
                    ganancia_año = round(total_año - inversion_año, 2)

                    datos_tabla.append({
                        'Año': año,
                        'Inversion_total': round(inversion_año, 2),
                        'Capital_final': total_año,
                        'Ganancia': ganancia_año
                    })

                # Renderizar resultados
                return render_template(
                    'index.html',
                    capitalfinal=capitalfinal,
                    ganancia=ganancia,
                    inversiontotal=inversiontotal,
                    datos_tabla=datos_tabla
                )
            except ValueError as e:
                flash(f'Error al realizar los cálculos. Por favor, revisa los datos ingresados. (Error: {e})')
                return redirect(url_for('index'))
        elif request.method == 'GET':
            return render_template('index.html', capitalfinal=None)

    return app

# Ejecutar la aplicación solo si el archivo se ejecuta directamente
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
