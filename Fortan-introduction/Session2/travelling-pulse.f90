PROGRAM travelling

    implicit none

    real, parameter :: delX=0.05, delT=0.05, c=1.0
    real, parameter :: Lx=1.0, Lt=1.0, x0=0.25, x1=0.75
    integer, parameter :: Nx = INT(Lx/delX), Nt = INT(Lt/delT)

    integer :: j, n, step
    real :: x
    real, dimension(Nt, Nx) :: array

    ! initialize
    DO j = 1, Nx
        x = (j-1)*delX
        if (x > x0 .AND. x < x1) then
            array(1,j) = 1.0
        else
            array(1,j) = 0.0
        end if
    END DO

    ! travelling wave
    DO n = 1, Nt
        step = INT(c * delT / delX)
        DO j = 1, Nx
            if (j == Nx) then ! boundary c0ndition (wrap around)
                array(n+1,1) = array(n,j)
            else                                ! if not at boundary
                array(n+1,j+step)= array(n,j)
            end if 
            
        END DO

    END DO

    ! write file
    open(10, file="travveling-pulse.txt", status="replace")
    do n = 1, Nt
        write(10, *) array(n, :)
    end do
    close(10)

    print*, "done"

END PROGRAM travelling