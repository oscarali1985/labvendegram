-- --------------------------------------------------------
-- Host:                         bcslpycfmnhs9gp1fcfb-mysql.services.clever-cloud.com
-- Server version:               8.0.15-5 - Exherbo
-- Server OS:                    Linux
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for bcslpycfmnhs9gp1fcfb
CREATE DATABASE IF NOT EXISTS `bcslpycfmnhs9gp1fcfb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `bcslpycfmnhs9gp1fcfb`;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.producto
CREATE TABLE IF NOT EXISTS `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `foto` varchar(200) NOT NULL,
  `descripcion` varchar(2000) NOT NULL,
  `precio` float NOT NULL,
  `cantidad` int(11) NOT NULL,
  `etiqueta_general` enum('PRODUCTOS','SERVICIOS') NOT NULL,
  `etiqueta_uno` enum('ALIMENTOS','BEBIDAS','CEREALES','DECORACIONES','DETERGENTES','ENLATADOS','JABONES','MANTENIMIENTOS','MAQUILLAJES','MEDICAMENTOS','PELUQUERIA','PELUQUERIA_VETERINARIA','PLOMERIA','REPARACIONES','ROPA','SALSAS') NOT NULL,
  `etiqueta_dos` enum('ALIMENTOS','BEBIDAS','CEREALES','DECORACIONES','DETERGENTES','ENLATADOS','JABONES','MANTENIMIENTOS','MAQUILLAJES','MEDICAMENTOS','PELUQUERIA','PELUQUERIA_VETERINARIA','PLOMERIA','REPARACIONES','ROPA','SALSAS') DEFAULT NULL,
  `etiqueta_tres` enum('ALIMENTOS','BEBIDAS','CEREALES','DECORACIONES','DETERGENTES','ENLATADOS','JABONES','MANTENIMIENTOS','MAQUILLAJES','MEDICAMENTOS','PELUQUERIA','PELUQUERIA_VETERINARIA','PLOMERIA','REPARACIONES','ROPA','SALSAS') DEFAULT NULL,
  `tienda_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `titulo` (`titulo`),
  KEY `tienda_id` (`tienda_id`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`tienda_id`) REFERENCES `tienda` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.producto: ~4 rows (approximately)
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` (`id`, `titulo`, `foto`, `descripcion`, `precio`, `cantidad`, `etiqueta_general`, `etiqueta_uno`, `etiqueta_dos`, `etiqueta_tres`, `tienda_id`) VALUES
	(1, 'Servicio Tecnico', 'null', 'Servicio PC2', 20, 10, 'SERVICIOS', 'MANTENIMIENTOS', NULL, 'REPARACIONES', 1),
	(2, 'Harina Pan', 'null', 'Venta de comida', 20, 10, 'PRODUCTOS', 'ALIMENTOS', NULL, NULL, 1),
	(3, 'Enlatados', 'null', 'Venta de comida', 20, 10, 'PRODUCTOS', 'ALIMENTOS', NULL, NULL, 1),
	(4, 'Canela', 'null', 'Venta de comida', 20, 10, 'PRODUCTOS', 'ALIMENTOS', NULL, NULL, 1),
	(5, 'lipton biggerdsata', 'foto', 'la', 20, 30, 'PRODUCTOS', 'ALIMENTOS', 'ENLATADOS', 'ALIMENTOS', 1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.tienda
CREATE TABLE IF NOT EXISTS `tienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_tienda` varchar(40) NOT NULL,
  `correo_tienda` varchar(30) NOT NULL,
  `telefono_tienda` varchar(30) DEFAULT NULL,
  `foto_tienda` varchar(200) DEFAULT NULL,
  `facebook_tienda` varchar(30) DEFAULT NULL,
  `instagram_tienda` varchar(30) DEFAULT NULL,
  `twitter_tienda` varchar(30) DEFAULT NULL,
  `zona_general` enum('DISTRITO_CAPITAL','MIRANDA') NOT NULL,
  `zona_uno` enum('ALTAGRACIA','ANTÍMANO','CANDELARIA','CARICUAO','CATEDRAL','CATIA','CAUCAGÜITA','CHACAO','COCHE','EL_CAFETAL','EL_JUNQUITO','EL_PARAÍSO','EL_RECREO','EL_VALLE','FILA_DE_MARICHES','LA_DOLORITA','LA_PASTORA','LA_VEGA','LAS_MINAS','LEONCIO_MARTÍNEZ','MACARAO','NUESTRA_SEÑORA_DEL_ROSARIO','PETARE','SAN_AGUSTÍN','SAN_BERNARDINO','SAN_JOSÉ','SAN_JUAN','SAN_PEDRO','SANTA_ROSALÍA','SANTA_ROSALÍA_DE_PALERMO','SANTA_TERESA','VEINTITRÉS_DE_ENERO') DEFAULT NULL,
  `zona_dos` enum('ALTAGRACIA','ANTÍMANO','CANDELARIA','CARICUAO','CATEDRAL','CATIA','CAUCAGÜITA','CHACAO','COCHE','EL_CAFETAL','EL_JUNQUITO','EL_PARAÍSO','EL_RECREO','EL_VALLE','FILA_DE_MARICHES','LA_DOLORITA','LA_PASTORA','LA_VEGA','LAS_MINAS','LEONCIO_MARTÍNEZ','MACARAO','NUESTRA_SEÑORA_DEL_ROSARIO','PETARE','SAN_AGUSTÍN','SAN_BERNARDINO','SAN_JOSÉ','SAN_JUAN','SAN_PEDRO','SANTA_ROSALÍA','SANTA_ROSALÍA_DE_PALERMO','SANTA_TERESA','VEINTITRÉS_DE_ENERO') DEFAULT NULL,
  `zona_tres` enum('ALTAGRACIA','ANTÍMANO','CANDELARIA','CARICUAO','CATEDRAL','CATIA','CAUCAGÜITA','CHACAO','COCHE','EL_CAFETAL','EL_JUNQUITO','EL_PARAÍSO','EL_RECREO','EL_VALLE','FILA_DE_MARICHES','LA_DOLORITA','LA_PASTORA','LA_VEGA','LAS_MINAS','LEONCIO_MARTÍNEZ','MACARAO','NUESTRA_SEÑORA_DEL_ROSARIO','PETARE','SAN_AGUSTÍN','SAN_BERNARDINO','SAN_JOSÉ','SAN_JUAN','SAN_PEDRO','SANTA_ROSALÍA','SANTA_ROSALÍA_DE_PALERMO','SANTA_TERESA','VEINTITRÉS_DE_ENERO') DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `tienda_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.tienda: ~1 rows (approximately)
/*!40000 ALTER TABLE `tienda` DISABLE KEYS */;
INSERT INTO `tienda` (`id`, `nombre_tienda`, `correo_tienda`, `telefono_tienda`, `foto_tienda`, `facebook_tienda`, `instagram_tienda`, `twitter_tienda`, `zona_general`, `zona_uno`, `zona_dos`, `zona_tres`, `usuario_id`) VALUES
	(1, 'Support OAMD', 'oamd@gmail.com', '414', NULL, 'oscarali', 'oscarali1985', NULL, 'DISTRITO_CAPITAL', 'CANDELARIA', NULL, NULL, 1);
/*!40000 ALTER TABLE `tienda` ENABLE KEYS */;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `nombre_usuario` varchar(20) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `correo` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `clave_hash` varchar(250) NOT NULL,
  `salt` varchar(16) NOT NULL,
  `foto_perfil` varchar(50) DEFAULT NULL,
  `administrador` tinyint(1) NOT NULL,
  `suscripcion` int(11) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.usuario: ~3 rows (approximately)
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` (`id`, `nombre`, `apellido`, `nombre_usuario`, `fecha_nacimiento`, `correo`, `telefono`, `clave_hash`, `salt`, `foto_perfil`, `administrador`, `suscripcion`, `fecha_registro`) VALUES
	(1, 'Oscar', 'Marino', 'oscarali', '1985-05-25', 'oscarali1985@gmail.com', '584126147743', 'pbkdf2:sha256:150000$MMzPQBBU$f30effe93ddc83b2d02eb46f37049d2a72125d6b135bb081166ff1128a7f5b7d', 'oFQ7bA==', 'Sinfoto', 1, NULL, '2020-10-06'),
	(2, 'Albany', 'Padron', 'ananyabellop', '1997-03-07', 'a.padron@gmail.com', '04122587430', 'pbkdf2:sha256:150000$TeuBWzDj$06c47b203d711e9e636d598426642a802f15b39beb2da5efe4be1de4b2bea1dc', 'YoYXuQ==', 'hola', 0, NULL, '2020-10-07'),
	(3, 'Alexandra', 'Padron', 'Alexpa', '2000-03-07', 'alex03@gmail.com', '04147182645', 'pbkdf2:sha256:150000$sptSTl2Z$6558d2cb5e651a6029b8eed4682269f279403966e0e7639ca431a70ef58e68e7', '3p94lg==', 'hola', 0, NULL, '2020-10-07'),
	(4, 'Francisco', 'Fossi', 'Francisco', '2000-02-05', 'fran@gmail.com', '04122587430', 'pbkdf2:sha256:150000$ULn6VWjk$52a92ef419a5e47d87cfe6d626ec4d96017fc2be5f4c806fd3b04e1bd0af01bb', 'FG8Dpw==', 'hola', 0, NULL, '2020-10-08');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
