-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-03-2026 a las 15:46:44
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `estudiantes`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `idEstudiante` int(11) NOT NULL,
  `NombreEstu` varchar(40) NOT NULL,
  `EdadEstu` int(11) DEFAULT NULL,
  `Carrera` varchar(40) DEFAULT NULL,
  `Nota1` decimal(3,1) DEFAULT NULL,
  `Nota2` decimal(3,1) DEFAULT NULL,
  `Nota3` decimal(3,1) DEFAULT NULL,
  `Promedio` decimal(3,1) DEFAULT NULL,
  `Desempeno` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`idEstudiante`, `NombreEstu`, `EdadEstu`, `Carrera`, `Nota1`, `Nota2`, `Nota3`, `Promedio`, `Desempeno`) VALUES
(1, 'Paula', 21, 'Fisica', 4.0, 4.0, 3.0, 3.0, 'Bueno'),
(2, 'Ana', 18, 'Ingenieria', 2.0, 5.0, 3.0, 3.0, 'regular'),
(3, 'Maria', 23, 'Ingenieria', 5.0, 4.0, 3.0, 4.0, 'Bueno'),
(4, 'Luis', 22, 'Matematicas', 2.0, 3.0, 4.0, 3.0, 'regular'),
(5, 'Ana', 21, 'Ingenieria', 5.0, 5.0, 5.0, 5.0, 'Excelente'),
(6, 'Maria', 23, 'Ingenieria', 4.0, 3.0, 3.0, 3.0, 'regular'),
(7, 'Ana', 20, 'Fisica', 2.0, 3.0, 3.0, 2.0, 'regular'),
(8, 'Luis', 20, 'Ingenieria', 4.0, 2.0, 4.0, 3.0, 'Bueno'),
(9, 'Luis', 23, 'Fisica', 4.0, 3.0, 2.0, 3.0, 'regular'),
(10, 'Luis', 22, 'Ingenieria', 3.0, 3.0, 2.0, 2.0, 'regular'),
(11, 'Ana', 20, 'Fisica', 5.0, 3.0, 2.0, 3.0, 'regular'),
(12, 'Carlos', 19, 'Fisica', 4.0, 2.0, 2.0, 2.0, 'regular'),
(13, 'Luis', 21, 'Fisica', 2.0, 5.0, 5.0, 4.0, 'Bueno'),
(14, 'Maria', 22, 'Fisica', 5.0, 2.0, 2.0, 3.0, 'regular'),
(15, 'Jose', 18, 'Fisica', 4.0, 3.0, 2.0, 3.0, 'regular'),
(16, 'Paula', 21, 'Fisica', 5.0, 4.0, 2.0, 3.0, 'Bueno'),
(17, 'Luis', 22, 'Ingenieria', 2.0, 3.0, 2.0, 2.0, 'Deficiente'),
(18, 'Maria', 22, 'Matematicas', 5.0, 5.0, 2.0, 4.0, 'Bueno'),
(19, 'Luis', 20, 'Matematicas', 5.0, 4.0, 5.0, 4.0, 'Excelente'),
(20, 'Ana', 22, 'Ingenieria', 2.0, 3.0, 4.0, 3.0, 'regular'),
(21, 'Ana', 20, 'Fisica', 3.0, 5.0, 2.0, 3.0, 'Bueno'),
(22, 'Carlos', 20, 'Ingenieria', 2.0, 4.0, 5.0, 3.0, 'Bueno'),
(23, 'Luis', 23, 'Fisica', 3.0, 2.0, 5.0, 3.0, 'Bueno'),
(24, 'Ana', 21, 'Ingenieria', 3.0, 5.0, 4.0, 4.0, 'Bueno'),
(25, 'Carlos', 19, 'Matematicas', 4.0, 3.0, 3.0, 3.0, 'regular'),
(26, 'Maria', 18, 'Fisica', 3.0, 3.0, 5.0, 3.0, 'Bueno'),
(27, 'Carlos', 22, 'Matematicas', 3.0, 4.0, 2.0, 3.0, 'regular'),
(28, 'Luis', 21, 'Ingenieria', 2.0, 3.0, 5.0, 3.0, 'regular'),
(29, 'Jose', 20, 'Matematicas', 4.0, 3.0, 3.0, 3.0, 'regular'),
(30, 'Ana', 19, 'Ingenieria', 3.0, 2.0, 3.0, 3.0, 'regular'),
(31, 'Maria', 18, 'Ingenieria', 5.0, 4.0, 4.0, 4.0, 'Excelente'),
(32, 'Maria', 23, 'Fisica', 2.0, 3.0, 4.0, 3.0, 'regular'),
(33, 'Jose', 18, 'Matematicas', 5.0, 3.0, 4.0, 4.0, 'Bueno'),
(34, 'Ana', 18, 'Matematicas', 5.0, 2.0, 5.0, 4.0, 'Bueno'),
(35, 'Jose', 20, 'Fisica', 2.0, 2.0, 2.0, 2.0, 'Deficiente'),
(36, 'Paula', 23, 'Fisica', 5.0, 5.0, 3.0, 4.0, 'Bueno'),
(37, 'Jose', 18, 'Fisica', 4.0, 3.0, 3.0, 3.0, 'Bueno'),
(38, 'Ana', 21, 'Fisica', 5.0, 3.0, 5.0, 4.0, 'Excelente'),
(39, 'Ana', 22, 'Ingenieria', 3.0, 5.0, 2.0, 3.0, 'Bueno'),
(40, 'Ana', 23, 'Fisica', 3.0, 2.0, 2.0, 2.0, 'regular'),
(41, 'Luis', 18, 'Fisica', 3.0, 3.0, 4.0, 3.0, 'Bueno'),
(42, 'Luis', 23, 'Fisica', 3.0, 4.0, 3.0, 3.0, 'Bueno'),
(43, 'Ana', 22, 'Fisica', 2.0, 5.0, 3.0, 3.0, 'regular'),
(44, 'Maria', 21, 'Fisica', 5.0, 5.0, 4.0, 4.0, 'Excelente'),
(45, 'Paula', 20, 'Matematicas', 2.0, 3.0, 2.0, 2.0, 'Deficiente'),
(46, 'Ana', 18, 'Fisica', 5.0, 2.0, 2.0, 3.0, 'regular'),
(47, 'Nicolasito', 19, 'Ingenieria', 5.0, 5.0, 5.0, 5.0, 'Excelente'),
(48, 'Nicolasito', 19, 'Ingenieria', 5.0, 5.0, 5.0, 5.0, 'Excelente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL,
  `UserName` varchar(40) NOT NULL,
  `PasswordUser` varchar(255) NOT NULL,
  `RolUsu` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idUsuario`, `UserName`, `PasswordUser`, `RolUsu`) VALUES
(1, 'Nicolas', '123', 'Admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`idEstudiante`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `idEstudiante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

DROP TABLE IF EXISTS `estudiantes`;
DROP TABLE IF EXISTS `usuarios`;