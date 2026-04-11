program lec3

        implicit none

        real(8) :: dt
        real(8) :: dx=0.25, c=1, cfl=0.9

        !namelist
        NAMELIST /grid/dx, cfl, c
        
        ! time step
        dt = cfl * dx / c
        print "(A7, F4.2, A5, F4.2)", "CFL", cfl, "dt: ", dt

        ! read file
        open(11,FILE="namelist_grid", status="old")
        read(11, grid)

        ! new time step
        dt = cfl * dx / c
        print "(A7, F4.2, A5, F4.2)", "CFL", cfl, "dt: ", dt

end program lec3