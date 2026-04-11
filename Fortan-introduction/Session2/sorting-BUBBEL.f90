PROGRAM sorting

    implicit none
    integer, parameter :: len=8
    integer :: i, k
    real :: rand, smaller, larger
    real(4), dimension(len) :: array 
    
    ! here we make a random array
    
    do i=1, len
        call random_number(rand)
        array(i) = rand*10
    end do

    print*, "Unsorted array"
    print '(F10.4)', array


    ! Do a bubbel sort
    DO k = 1, len-1

        do i = 1, len-k
            if (array(i)-array(i+1)>0) then
                smaller = array(i+1)
                larger = array(i)
                array(i) = smaller
                array(i+1) = larger
            else 
        end if

        end do


    ENDDO

    print*, "Sorted array"
    print '(F10.4)', array

END PROGRAM sorting