/*
 MLX90614 sensor read from Raspberyy I2C

 Copyright 2016  Oleg Kutkov <elenbert@gmail.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.  
*/

#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <getopt.h>
#include <stdlib.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <errno.h>
#include "Mlx_addrs.h"

/* Just in case */ 
#ifndef I2C_SMBUS_READ
#define I2C_SMBUS_READ 1
#endif
#ifndef I2C_SMBUS_WRITE
#define I2C_SMBUS_WRITE 0
#endif

// buffer for data reading or writing
typedef union i2c_smbus_data i2c_data;


static int DEBUG_MODE = 0;

extern const char* __progname;
///

int GetDevice(const int bus_num, const unsigned char i2c_addr)
{
	char dev_path[11] = { 0 };

	// construct path to i2c device
	snprintf(dev_path, 11, "/dev/i2c-%i", bus_num);

	if (DEBUG_MODE) {
		fprintf(stderr, "Opening i2c interface %s\n", dev_path);
	}

	int fdev = open(dev_path, O_RDWR);

	if (fdev < 0) {
		fprintf(stderr, "Failed to open I2C interface %s Error: %s\n", dev_path, strerror(errno));
		return -1;
	}

	if (DEBUG_MODE) {
		fprintf(stderr, "Setting up slave address 0x%02X\n", i2c_addr);
	}

	// set addr of the slave i2c device
	if (ioctl(fdev, I2C_SLAVE, i2c_addr) < 0) {
		fprintf(stderr, "Failed to select I2C slave device! Error: %s\n", strerror(errno));
		return -1;
	}

	// enable checksums
	if (ioctl(fdev, I2C_PEC, 1) < 0) {
		fprintf(stderr, "Failed to enable SMBus packet error checking, error: %s\n", strerror(errno));
		return -1;
	}

	return fdev;
}

int TalkToDevice(const int fdev, const int read, const char command, i2c_data* data)
{
	// initialize i2c_smus structure for combined write/read request to device
	struct i2c_smbus_ioctl_data sdat = {
		.read_write = (read ? I2C_SMBUS_READ : I2C_SMBUS_WRITE), // set operation type: read or write
		.command = command,		// set command, i.e. register number
		.size = I2C_SMBUS_WORD_DATA,   // set data size, note: mlx supports only WORD
		.data = data    // pointer to data
	};

	if (DEBUG_MODE) {
		fprintf(stderr, "Perfoming %s request to device, command = 0x%02X\n"
						, (read ? "I2C_SMBUS_READ" : "I2C_SMBUS_WRITE"), command);
	}

	// perfom combined request to device
	if (ioctl(fdev, I2C_SMBUS, &sdat) < 0) {
		fprintf(stderr, "Failed to perfom I2C_SMBUS transaction, error: %s\n", strerror(errno));
		return -1;
	}

	if (DEBUG_MODE) {
		fprintf(stderr, "Ok, got answer from device\n");
	}

	return 0;
}


double ReadData(const int fdev, const char command)
{	
	i2c_data data;
	if (TalkToDevice(fdev, 1, command, &data) < 0) {
		return  -999;
	}
	double temp = 0;
	temp = (double) data.word;
	temp = (temp * 0.02)-0.01;
	temp = temp - 273.15;
	return temp;
}



int Main()
{
	int busNumber = 1;
	unsigned char i2c_addr = MLX90614_I2CADDR;
	int fdev = GetDevice(busNumber, i2c_addr);
	double res = ReadData(fdev, MLX90614_TOBJ1);
	close(fdev);
	return res;
}

