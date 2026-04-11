FC = gfortran
FF = -g -O3  -fbounds-check -fbacktrace

NCDF_ROOT = /usr
LIB = -L$(NCDF_ROOT)/lib -lnetcdf -lnetcdff

NAME = hello-world.f90
TARGET = hello-world.x

All: $(TARGET)

$(TARGET): $(NAME)
	$(FC) $(FF) -o $(TARGET) $(NAME) -I$(NCDF_ROOT)/include $(LIB)

hej:
	@echo hej!

clean:
	rm -f *.x *.bin *.mod *~ *\#