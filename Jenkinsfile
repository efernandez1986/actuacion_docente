pipeline {
  agent any
  stages {
    stage('cp') {
      steps {
        sh '''GITHUB_REPO_URL="https://github.com/efernandez1986/actuacion_docente.git"
CARPETA_A_COPIAR="https://github.com/efernandez1986/actuacion_docente/tree/main/teaching_performance"
ODOO_CONTAINER_NAME="odoo17"
DEST_DIR="/opt/odoo17/odoo/localaddons"

# Clonar el repositorio de GitHub
git clone $GITHUB_REPO_URL repositorio_temp

# Copiar la carpeta al contenedor de Odoo
docker cp repositorio_temp/$CARPETA_A_COPIAR $ODOO_CONTAINER_NAME:$DEST_DIR

# Limpiar el repositorio clonado temporal
rm -rf repositorio_temp'''
      }
    }

  }
}